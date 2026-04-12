(function attachIrisSovereignCoreUtils(globalScope) {
  // Burgess Compliance: connectivity helpers tune local advisory behavior and queueing
  // without making medical claims or turning automation into decision authority.
  const existing = globalScope.IrisSovereignCore || {};
  const types = existing.types || {};
  const CONNECTIVITY_PROFILES = types.CONNECTIVITY_PROFILES || {
    STARLINK_HARDWIRED: 'starlink_hardwired',
    FIBER_HARDWIRED: 'fiber_hardwired',
    OTHER: 'other',
  };
  // Treat sustained ~900ms RTT as the point where background sync should prefer queueing.
  const SLOW_NETWORK_RTT_THRESHOLD_MS = 900;
  const PERIODIC_SYNC_INTERVALS_MS = Object.freeze({
    DEFAULT: 12 * 60 * 60 * 1000,
    FIBER_HARDWIRED: 4 * 60 * 60 * 1000,
    STARLINK_HARDWIRED: 18 * 60 * 60 * 1000,
    BALANCED_OTHER: 8 * 60 * 60 * 1000,
  });

  function canonicalize(value) {
    if (Array.isArray(value)) {
      return `[${value.map(item => canonicalize(item)).join(',')}]`;
    }
    if (value && typeof value === 'object') {
      return `{${Object.keys(value).sort().map(key => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
    }
    return JSON.stringify(value);
  }

  function normalizeConnectivityProfile(value = '') {
    const raw = String(value || '').trim().toLowerCase();
    if (!raw) return CONNECTIVITY_PROFILES.OTHER;
    if (['starlink_hardwired', 'starlink_ethernet', 'starlink'].includes(raw)) return CONNECTIVITY_PROFILES.STARLINK_HARDWIRED;
    if (['fiber_hardwired', 'fiber', 'fiber_optic', 'fiber optic'].includes(raw)) return CONNECTIVITY_PROFILES.FIBER_HARDWIRED;
    return CONNECTIVITY_PROFILES.OTHER;
  }

  function connectivityProfileLabel(value = '') {
    const normalized = normalizeConnectivityProfile(value);
    if (normalized === CONNECTIVITY_PROFILES.STARLINK_HARDWIRED) return 'Starlink Hardwired';
    if (normalized === CONNECTIVITY_PROFILES.FIBER_HARDWIRED) return 'Fiber Hardwired';
    return 'Other';
  }

  function normalizeNetworkSnapshot(snapshot = {}) {
    return {
      online: snapshot.online !== false,
      connection_type: String(snapshot.connection_type || snapshot.type || '').toLowerCase(),
      effective_type: String(snapshot.effective_type || snapshot.effectiveType || '').toLowerCase(),
      downlink_mbps: Number(snapshot.downlink_mbps ?? snapshot.downlink ?? 0) || 0,
      rtt_ms: Number(snapshot.rtt_ms ?? snapshot.rtt ?? 0) || 0,
      save_data: Boolean(snapshot.save_data ?? snapshot.saveData),
      wired_detected: Boolean(snapshot.wired_detected),
      updated_at: snapshot.updated_at || new Date().toISOString(),
    };
  }

  function captureNetworkSnapshot(connection, online = true) {
    const type = String(connection && connection.type || '').toLowerCase();
    const effectiveType = String(connection && connection.effectiveType || '').toLowerCase();
    return normalizeNetworkSnapshot({
      online,
      connection_type: type,
      effective_type: effectiveType,
      downlink_mbps: connection && typeof connection.downlink === 'number' ? connection.downlink : 0,
      rtt_ms: connection && typeof connection.rtt === 'number' ? connection.rtt : 0,
      save_data: Boolean(connection && connection.saveData),
      wired_detected: type === 'ethernet',
    });
  }

  function addConnectivityTagsFromText(value, tags) {
    const lower = String(value || '').toLowerCase();
    if (!lower) return tags;
    if (/(^|\W)starlink(\W|$)/.test(lower)) tags.add('starlink');
    if (/(^|\W)fiber(\W|$)/.test(lower)) tags.add('fiber');
    if (/(^|\W)ont(\W|$)/.test(lower)) tags.add('ont');
    if (/(^|\W)ethernet(\W|$)|(^|\W)wired(\W|$)|(^|\W)hardwired(\W|$)/.test(lower)) tags.add('ethernet');
    if (/fixed wireless/.test(lower)) tags.add('fixed-wireless');
    if (/(^|\W)dsl(\W|$)/.test(lower)) tags.add('dsl');
    if (/(^|\W)cable(\W|$)/.test(lower)) tags.add('cable');
    if (/bypass mode/.test(lower)) tags.add('bypass-mode');
    if (/wi-?fi off|wifi off/.test(lower)) tags.add('wifi-off');
    if (/manual sync|queued sync|queued manual sync/.test(lower)) tags.add('queued-sync');
    return tags;
  }

  function buildConnectivityTags(preferences = {}, extraText = '') {
    const tags = new Set(['environment', 'connectivity']);
    const normalized = normalizeConnectivityProfile(preferences.connectivity_profile);
    if (normalized === CONNECTIVITY_PROFILES.STARLINK_HARDWIRED) {
      tags.add('starlink');
      tags.add('ethernet');
      tags.add('hardwired');
    } else if (normalized === CONNECTIVITY_PROFILES.FIBER_HARDWIRED) {
      tags.add('fiber');
      tags.add('ont');
      tags.add('ethernet');
      tags.add('hardwired');
    } else {
      tags.add('other-link');
    }
    if (preferences.minimize_wireless || preferences.low_wireless_mode) tags.add('minimized-wireless');
    if (preferences.prefer_queued_syncs) tags.add('queued-sync');
    addConnectivityTagsFromText(preferences.environmental_note || preferences.connectivity_note || '', tags);
    addConnectivityTagsFromText(extraText, tags);
    return Array.from(tags);
  }

  function summarizeEnvironment(preferences = {}) {
    const parts = [];
    const normalized = normalizeConnectivityProfile(preferences.connectivity_profile);
    if (normalized === CONNECTIVITY_PROFILES.STARLINK_HARDWIRED) parts.push('Starlink hardwired selected for local review');
    if (normalized === CONNECTIVITY_PROFILES.FIBER_HARDWIRED) parts.push('Fiber hardwired selected for local review');
    if (normalized === CONNECTIVITY_PROFILES.OTHER) parts.push('Other connectivity profile selected for local review');
    if (preferences.minimize_wireless || preferences.low_wireless_mode) parts.push('minimized local wireless environment requested');
    if (preferences.prefer_queued_syncs) parts.push('queued/manual sync preference enabled');
    if (preferences.environmental_note || preferences.connectivity_note) parts.push(preferences.environmental_note || preferences.connectivity_note);
    return parts.join('; ');
  }

  function createTriggerTemplatePresets() {
    return {
      starlink_hardwired_review: {
        natural_language: 'Every 12 hours, remind me to review whether Starlink is still hardwired with Ethernet, Wi-Fi is off where I want it off, and Hub Mode can stay queued until I choose a manual sync.',
        label: 'Starlink hardwired review',
        type: 'periodic',
        interval_hours: 12,
        detection_sources: ['conversation'],
        keywords: ['starlink', 'ethernet', 'bypass mode', 'wifi off'],
        description: 'Advisory review for a user-configured lower-local-wireless setup. Human review remains required for any actual adjustment.',
      },
      fiber_hardwired_review: {
        natural_language: 'Every 24 hours, remind me to review whether fiber is still hardwired from the ONT to Ethernet, local Wi-Fi is only on when I choose it, and Iris can stay offline-first between queued syncs.',
        label: 'Fiber hardwired review',
        type: 'periodic',
        interval_hours: 24,
        detection_sources: ['conversation'],
        keywords: ['fiber', 'ont', 'ethernet', 'hardwired'],
        description: 'Advisory review for a fiber ONT plus Ethernet setup where the user wants the lowest local wireless routine available.',
      },
      connectivity_profile_checkin: {
        natural_language: 'Every 24 hours, remind me to compare whether Starlink hardwired or fiber hardwired is the better fit for my current voice-first work, queued sync routine, and personal environmental preferences.',
        label: 'Connectivity profile check-in (Starlink vs Fiber)',
        type: 'periodic',
        interval_hours: 24,
        detection_sources: ['conversation'],
        keywords: ['starlink', 'fiber', 'ethernet', 'ont', 'manual sync'],
        description: 'Creates a calm comparison prompt so the user can review which hardwired profile best matches current availability, latency, and environmental preferences.',
      },
      environmental_note_wired_setup: {
        natural_language: 'If conversation, clipboard, or page text mentions fiber, Starlink, ONT, Ethernet, bypass mode, fixed wireless, DSL, cable, or Wi-Fi off, queue a local prompt to commit an environmental note on the wired setup.',
        label: 'Environmental note on wired setup',
        type: 'keyword',
        interval_hours: 24,
        detection_sources: ['conversation', 'clipboard', 'page'],
        keywords: ['fiber', 'starlink', 'ont', 'ethernet', 'bypass mode', 'fixed wireless', 'dsl', 'cable', 'wifi off'],
        description: 'Queues a local prompt to capture a signed environmental note about a wired setup, sync preference, and later human review.',
      },
      connectivity_environment_log: {
        natural_language: 'If conversation, clipboard, or page text mentions Starlink, fiber, ONT, Ethernet, bypass mode, Wi-Fi off, dish placement, or cellular fallback, queue a local environmental review prompt.',
        label: 'Connectivity log for environmental review',
        type: 'keyword',
        interval_hours: 24,
        detection_sources: ['conversation', 'clipboard', 'page'],
        keywords: ['starlink', 'fiber', 'ont', 'ethernet', 'bypass mode', 'wifi off', 'dish placement', 'cellular fallback'],
        description: 'Creates a calm local prompt to log connectivity changes, accessibility context, or personal environmental preferences.',
      },
      assistive_setup_checkin: {
        natural_language: 'Every 24 hours, remind me to review whether my connectivity setup still supports voice use, focus, and reasonable adjustments for my needs.',
        label: 'Assistive setup check-in',
        type: 'periodic',
        interval_hours: 24,
        detection_sources: ['conversation'],
        keywords: ['reasonable adjustment', 'accessibility', 'voice', 'environment'],
        description: 'Periodic assistive-tech check-in for a sovereign setup. Advisory only and never a medical claim.',
      },
    };
  }

  function buildSovereignSyncPolicy(profile = {}, networkSnapshot = {}, options = {}) {
    const normalizedProfile = normalizeConnectivityProfile(profile.connectivity_profile);
    const snapshot = normalizeNetworkSnapshot(networkSnapshot);
    const online = snapshot.online;
    const saveData = snapshot.save_data;
    const networkSlow = ['slow-2g', '2g'].includes(snapshot.effective_type) || (snapshot.rtt_ms > SLOW_NETWORK_RTT_THRESHOLD_MS && snapshot.rtt_ms !== 0);
    const wiredPreferred = normalizedProfile === CONNECTIVITY_PROFILES.FIBER_HARDWIRED || normalizedProfile === CONNECTIVITY_PROFILES.STARLINK_HARDWIRED;
    const wiredDetected = snapshot.wired_detected || snapshot.connection_type === 'ethernet';
    let mode = 'queued';
    let allowBackgroundFlush = false;
    let periodicSyncMs = PERIODIC_SYNC_INTERVALS_MS.DEFAULT;

    if (normalizedProfile === CONNECTIVITY_PROFILES.FIBER_HARDWIRED && online && !saveData && !networkSlow) {
      mode = 'balanced';
      allowBackgroundFlush = true;
      periodicSyncMs = PERIODIC_SYNC_INTERVALS_MS.FIBER_HARDWIRED;
    } else if (normalizedProfile === CONNECTIVITY_PROFILES.STARLINK_HARDWIRED) {
      mode = profile.prefer_queued_syncs === false && online ? 'balanced' : 'queued';
      allowBackgroundFlush = online && wiredDetected && !networkSlow && !saveData && profile.prefer_queued_syncs === false;
      periodicSyncMs = PERIODIC_SYNC_INTERVALS_MS.STARLINK_HARDWIRED;
    } else if (online && !networkSlow && !saveData && profile.prefer_queued_syncs === false) {
      mode = 'balanced';
      allowBackgroundFlush = true;
      periodicSyncMs = PERIODIC_SYNC_INTERVALS_MS.BALANCED_OTHER;
    }

    if (!online) {
      mode = 'offline';
      allowBackgroundFlush = false;
    }

    if (options.forceManual || profile.governance && profile.governance.manual_sync_first) {
      allowBackgroundFlush = allowBackgroundFlush && mode !== 'queued';
    }

    return {
      mode,
      online,
      wired_preferred: wiredPreferred,
      wired_detected: wiredDetected,
      allow_background_flush: allowBackgroundFlush,
      prefer_queue_registration: mode === 'queued' || !online,
      periodic_sync_ms: periodicSyncMs,
      advisory: summarizeEnvironment(profile) || 'Stay local-first and queue commitment syncs until the user consents to delivery.',
    };
  }

  globalScope.IrisSovereignCore = {
    ...existing,
    utils: {
      ...(existing.utils || {}),
      canonicalize,
      normalizeConnectivityProfile,
      connectivityProfileLabel,
      normalizeNetworkSnapshot,
      captureNetworkSnapshot,
      buildConnectivityTags,
      summarizeEnvironment,
      createTriggerTemplatePresets,
      buildSovereignSyncPolicy,
      addConnectivityTagsFromText,
    },
  };
})(typeof globalThis !== 'undefined' ? globalThis : self);
