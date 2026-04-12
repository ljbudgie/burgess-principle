(function attachIrisSovereigntyProfileManager(globalScope) {
  // Burgess Compliance: the sovereignty profile captures user-controlled preferences
  // for local operation and export boundaries; it never auto-resolves the Burgess test.
  const existing = globalScope.IrisSovereignCore || {};
  const types = existing.types || {};
  const utils = existing.utils || {};
  const SETTINGS_KEYS = types.SETTINGS_KEYS || {
    SOVEREIGNTY_PROFILE: 'user-sovereignty-profile',
    NETWORK_SNAPSHOT: 'user-sovereignty-network-snapshot',
    LEGACY_HUB_CONFIG: 'hub-config-v2',
  };
  const cloneDefault = types.cloneDefaultSovereigntyProfile || (() => ({
    version: 1,
    connectivity_profile: 'other',
    minimize_wireless: false,
    prefer_queued_syncs: true,
    trigger_sensitivity: 'balanced',
    governance: {
      manual_sync_first: true,
      memory_background_unlock: false,
      trigger_background_unlock: false,
      receipt_export_requires_user_action: true,
    },
    environmental_note: '',
    network_snapshot: null,
    updated_at: '',
    last_updated_by: 'system-default',
    profile_fingerprint: '',
  }));

  function normalizeProfile(profile = {}) {
    const base = cloneDefault();
    return {
      ...base,
      ...profile,
      connectivity_profile: utils.normalizeConnectivityProfile ? utils.normalizeConnectivityProfile(profile.connectivity_profile || base.connectivity_profile) : (profile.connectivity_profile || base.connectivity_profile),
      minimize_wireless: Boolean(profile.minimize_wireless ?? profile.low_wireless_mode ?? base.minimize_wireless),
      prefer_queued_syncs: Boolean(profile.prefer_queued_syncs ?? base.prefer_queued_syncs),
      environmental_note: String(profile.environmental_note || profile.connectivity_note || base.environmental_note || ''),
      governance: {
        ...base.governance,
        ...(profile.governance || {}),
      },
      network_snapshot: profile.network_snapshot ? utils.normalizeNetworkSnapshot(profile.network_snapshot) : base.network_snapshot,
      updated_at: profile.updated_at || base.updated_at,
      last_updated_by: profile.last_updated_by || base.last_updated_by,
      profile_fingerprint: profile.profile_fingerprint || '',
    };
  }

  function createProfileManager({ storage, sha256Hex, canonicalize, now = () => new Date().toISOString() }) {
    if (!storage || typeof storage.getSetting !== 'function' || typeof storage.saveSetting !== 'function') {
      throw new Error('Profile manager requires getSetting/saveSetting storage adapters.');
    }

    async function persistProfile(profile) {
      const normalized = normalizeProfile(profile);
      if (sha256Hex && canonicalize) {
        normalized.profile_fingerprint = await sha256Hex(canonicalize({
          connectivity_profile: normalized.connectivity_profile,
          minimize_wireless: normalized.minimize_wireless,
          prefer_queued_syncs: normalized.prefer_queued_syncs,
          trigger_sensitivity: normalized.trigger_sensitivity,
          governance: normalized.governance,
          environmental_note: normalized.environmental_note,
        }));
      }
      await storage.saveSetting(SETTINGS_KEYS.SOVEREIGNTY_PROFILE, normalized);
      return normalized;
    }

    async function loadProfile() {
      const saved = await storage.getSetting(SETTINGS_KEYS.SOVEREIGNTY_PROFILE);
      if (saved && typeof saved === 'object') {
        return normalizeProfile(saved);
      }
      const legacyHubConfig = await storage.getSetting(SETTINGS_KEYS.LEGACY_HUB_CONFIG);
      if (legacyHubConfig && typeof legacyHubConfig === 'object') {
        return normalizeProfile({
          connectivity_profile: legacyHubConfig.connectivity_profile,
          minimize_wireless: legacyHubConfig.low_wireless_mode,
          prefer_queued_syncs: legacyHubConfig.prefer_queued_syncs,
          environmental_note: legacyHubConfig.connectivity_note,
        });
      }
      return normalizeProfile();
    }

    async function saveProfile(patch = {}, source = 'manual-update') {
      const current = await loadProfile();
      return persistProfile({
        ...current,
        ...patch,
        updated_at: now(),
        last_updated_by: source,
      });
    }

    async function syncHubPreferences(hubConfig = {}) {
      return saveProfile({
        connectivity_profile: hubConfig.connectivity_profile,
        minimize_wireless: hubConfig.low_wireless_mode,
        prefer_queued_syncs: hubConfig.prefer_queued_syncs,
        environmental_note: hubConfig.connectivity_note,
      }, 'hub-preferences');
    }

    async function syncGovernancePreferences(governance = {}) {
      const current = await loadProfile();
      return persistProfile({
        ...current,
        governance: {
          ...current.governance,
          ...governance,
        },
        updated_at: now(),
        last_updated_by: 'governance-preferences',
      });
    }

    async function saveNetworkSnapshot(snapshot = {}) {
      const normalized = utils.normalizeNetworkSnapshot ? utils.normalizeNetworkSnapshot(snapshot) : snapshot;
      await storage.saveSetting(SETTINGS_KEYS.NETWORK_SNAPSHOT, normalized);
      return saveProfile({ network_snapshot: normalized }, 'network-snapshot');
    }

    async function getNetworkSnapshot() {
      return await storage.getSetting(SETTINGS_KEYS.NETWORK_SNAPSHOT);
    }

    async function getSyncPolicy(options = {}) {
      const profile = await loadProfile();
      const networkSnapshot = profile.network_snapshot || await getNetworkSnapshot() || {};
      return utils.buildSovereignSyncPolicy
        ? utils.buildSovereignSyncPolicy(profile, networkSnapshot, options)
        : { mode: profile.prefer_queued_syncs ? 'queued' : 'balanced', allow_background_flush: false };
    }

    return {
      loadProfile,
      saveProfile,
      syncHubPreferences,
      syncGovernancePreferences,
      saveNetworkSnapshot,
      getNetworkSnapshot,
      getSyncPolicy,
      normalizeProfile,
    };
  }

  globalScope.IrisSovereignCore = {
    ...existing,
    createProfileManager,
    profile: {
      ...(existing.profile || {}),
      createProfileManager,
      normalizeProfile,
    },
  };
})(typeof globalThis !== 'undefined' ? globalThis : self);
