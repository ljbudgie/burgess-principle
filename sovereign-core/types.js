(function attachIrisSovereignCoreTypes(globalScope) {
  // Burgess Compliance: shared sovereignty types describe local evidence policy only;
  // they never substitute for a named human reviewing the specific facts.
  const existing = globalScope.IrisSovereignCore || {};

  const CONNECTIVITY_PROFILES = Object.freeze({
    STARLINK_HARDWIRED: 'starlink_hardwired',
    FIBER_HARDWIRED: 'fiber_hardwired',
    OTHER: 'other',
  });

  const SETTINGS_KEYS = Object.freeze({
    SOVEREIGNTY_PROFILE: 'user-sovereignty-profile',
    NETWORK_SNAPSHOT: 'user-sovereignty-network-snapshot',
    LEGACY_HUB_CONFIG: 'hub-config-v2',
  });

  const DEFAULT_SOVEREIGNTY_PROFILE = Object.freeze({
    version: 1,
    connectivity_profile: CONNECTIVITY_PROFILES.OTHER,
    minimize_wireless: false,
    prefer_queued_syncs: true,
    trigger_sensitivity: 'balanced',
    governance: Object.freeze({
      manual_sync_first: true,
      memory_background_unlock: false,
      trigger_background_unlock: false,
      receipt_export_requires_user_action: true,
    }),
    environmental_note: '',
    network_snapshot: null,
    updated_at: '',
    last_updated_by: 'system-default',
    profile_fingerprint: '',
  });

  function cloneDefaultSovereigntyProfile() {
    return {
      ...DEFAULT_SOVEREIGNTY_PROFILE,
      governance: { ...DEFAULT_SOVEREIGNTY_PROFILE.governance },
    };
  }

  globalScope.IrisSovereignCore = {
    ...existing,
    types: {
      ...(existing.types || {}),
      CONNECTIVITY_PROFILES,
      SETTINGS_KEYS,
      DEFAULT_SOVEREIGNTY_PROFILE,
      cloneDefaultSovereigntyProfile,
    },
  };
})(typeof globalThis !== 'undefined' ? globalThis : self);
