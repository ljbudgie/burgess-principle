/**
 * share_truth.js — Social Propagation Module
 * Burgess Principle: Broadcast the Truth
 */
(function () {
    'use strict';

    var REPO_URL = 'https://github.com/ljbudgie/Burgessprinciple';
    var SHARE_MSG = 'I have deployed the Burgess Principle. My inbox is sovereign. The warrant is void. Get the code: ' + REPO_URL + ' #Sovereignty';

    var PLATFORMS = [
        {
            id: 'x',
            label: 'X (Twitter)',
            icon: '𝕏',
            url: function () {
                return 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(SHARE_MSG);
            }
        },
        {
            id: 'whatsapp',
            label: 'WhatsApp',
            icon: '💬',
            url: function () {
                return 'https://wa.me/?text=' + encodeURIComponent(SHARE_MSG);
            }
        },
        {
            id: 'telegram',
            label: 'Telegram',
            icon: '✈',
            url: function () {
                return 'https://t.me/share/url?url=' + encodeURIComponent(REPO_URL) +
                    '&text=' + encodeURIComponent(SHARE_MSG);
            }
        }
    ];

    function injectStyles() {
        var css = [
            '#bp-float-btn{',
            '  position:fixed;bottom:28px;right:28px;z-index:10000;',
            '  background:#00ff41;color:#0a0a0a;border:none;cursor:pointer;',
            '  font-family:"Roboto Mono","Courier New",monospace;font-size:0.875em;',
            '  letter-spacing:0.15em;text-transform:uppercase;padding:13px 22px;',
            '  box-shadow:0 0 20px rgba(0,255,65,0.5);transition:box-shadow 0.2s;',
            '  display:flex;align-items:center;gap:8px;',
            '}',
            '#bp-float-btn:hover{box-shadow:0 0 36px rgba(0,255,65,0.8);}',
            '#bp-modal-overlay{',
            '  display:none;position:fixed;inset:0;z-index:10001;',
            '  background:rgba(0,0,0,0.82);align-items:center;justify-content:center;',
            '}',
            '#bp-modal-overlay.open{display:flex;}',
            '#bp-modal{',
            '  background:#111;border:1px solid #1a2a1a;max-width:520px;width:90%;',
            '  padding:32px 28px;position:relative;',
            '  box-shadow:0 0 40px rgba(0,255,65,0.15);',
            '}',
            '#bp-modal-close{',
            '  position:absolute;top:12px;right:16px;background:none;border:none;',
            '  color:#6a8a6a;font-size:1.2em;cursor:pointer;line-height:1;',
            '}',
            '#bp-modal-close:hover{color:#00ff41;}',
            '#bp-modal-title{',
            '  font-family:"Cinzel","Times New Roman",serif;color:#ffd700;',
            '  font-size:1em;letter-spacing:0.15em;text-transform:uppercase;',
            '  margin-bottom:16px;',
            '}',
            '#bp-modal-msg{',
            '  font-family:"Roboto Mono","Courier New",monospace;font-size:0.875em;',
            '  color:#c8d8c8;border:1px solid #1a2a1a;padding:14px 16px;',
            '  margin-bottom:20px;line-height:1.6;background:#0a0a0a;',
            '}',
            '.bp-share-btn{',
            '  display:flex;align-items:center;gap:10px;width:100%;',
            '  padding:12px 18px;margin-bottom:10px;cursor:pointer;',
            '  font-family:"Roboto Mono","Courier New",monospace;font-size:0.875em;',
            '  letter-spacing:0.12em;text-transform:uppercase;text-decoration:none;',
            '  background:transparent;border:1px solid #1a2a1a;color:#c8d8c8;',
            '  transition:border-color 0.2s,color 0.2s;',
            '}',
            '.bp-share-btn:hover{border-color:#00ff41;color:#00ff41;}',
            '.bp-share-btn:last-child{margin-bottom:0;}',
        ].join('');
        var s = document.createElement('style');
        s.textContent = css;
        document.head.appendChild(s);
    }

    function buildModal() {
        var overlay = document.createElement('div');
        overlay.id = 'bp-modal-overlay';
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('aria-label', 'Broadcast the Truth');

        var modal = document.createElement('div');
        modal.id = 'bp-modal';

        var closeBtn = document.createElement('button');
        closeBtn.id = 'bp-modal-close';
        closeBtn.textContent = '✕';
        closeBtn.setAttribute('aria-label', 'Close');

        var title = document.createElement('div');
        title.id = 'bp-modal-title';
        title.textContent = '📡 Broadcast the Truth';

        var msgBox = document.createElement('div');
        msgBox.id = 'bp-modal-msg';
        msgBox.textContent = SHARE_MSG;

        modal.appendChild(closeBtn);
        modal.appendChild(title);
        modal.appendChild(msgBox);

        PLATFORMS.forEach(function (p) {
            var a = document.createElement('a');
            a.className = 'bp-share-btn';
            a.href = p.url();
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.setAttribute('data-platform', p.id);
            var iconSpan = document.createElement('span');
            iconSpan.textContent = p.icon;
            var labelSpan = document.createElement('span');
            labelSpan.textContent = 'Share on ' + p.label;
            a.appendChild(iconSpan);
            a.appendChild(labelSpan);
            modal.appendChild(a);
        });

        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) closeModal();
        });
    }

    function buildFloatButton() {
        var btn = document.createElement('button');
        btn.id = 'bp-float-btn';
        btn.setAttribute('aria-label', 'Broadcast the Truth');
        var iconSpan = document.createElement('span');
        iconSpan.textContent = '📡';
        var labelSpan = document.createElement('span');
        labelSpan.textContent = 'Broadcast the Truth';
        btn.appendChild(iconSpan);
        btn.appendChild(labelSpan);
        btn.addEventListener('click', openModal);
        document.body.appendChild(btn);
    }

    function openModal() {
        var overlay = document.getElementById('bp-modal-overlay');
        if (overlay) {
            overlay.classList.add('open');
            var closeBtn = document.getElementById('bp-modal-close');
            if (closeBtn) closeBtn.focus();
        }
    }

    function closeModal() {
        var overlay = document.getElementById('bp-modal-overlay');
        if (overlay) overlay.classList.remove('open');
        var floatBtn = document.getElementById('bp-float-btn');
        if (floatBtn) floatBtn.focus();
    }

    function init() {
        injectStyles();
        buildModal();
        buildFloatButton();
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') closeModal();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
