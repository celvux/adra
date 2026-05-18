/* Direct browser-to-S3 upload for Django admin image fields.
 * Uploads via a pre-signed PUT URL, bypassing the Vercel function timeout.
 */
(function () {
    'use strict';

    var PRESIGN_URL = '/admin/upload-presign/';

    function getCsrf() {
        var el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }

    function initWidget(fileInput) {
        var wrapper = fileInput.closest('.s3-upload-wrapper');
        if (!wrapper) return;
        var hiddenKey = wrapper.querySelector('input[type="hidden"][name^="_s3key_"]');
        var status = wrapper.querySelector('.s3-upload-status');
        if (!hiddenKey) return;

        fileInput.addEventListener('change', function () {
            var file = this.files[0];
            if (!file) return;

            status.textContent = 'Envoi en cours…';
            status.style.color = '#CE1126';
            fileInput.disabled = true;

            var fd = new FormData();
            fd.append('filename', file.name);
            fd.append('content_type', file.type);
            fd.append('folder', fileInput.dataset.folder || 'uploads');
            fd.append('csrfmiddlewaretoken', getCsrf());

            fetch(PRESIGN_URL, { method: 'POST', body: fd })
                .then(function (r) {
                    if (!r.ok) throw new Error('Erreur serveur (' + r.status + ')');
                    return r.json();
                })
                .then(function (data) {
                    if (data.error) throw new Error(data.error);
                    return fetch(data.url, {
                        method: 'PUT',
                        body: file,
                        headers: { 'Content-Type': file.type },
                    }).then(function (r) {
                        if (!r.ok) throw new Error('Échec envoi S3 (' + r.status + ')');
                        return data.key;
                    });
                })
                .then(function (key) {
                    hiddenKey.value = key;
                    status.textContent = '✓ Image envoyée — cliquez Enregistrer pour valider.';
                    status.style.color = '#28a745';
                })
                .catch(function (err) {
                    status.textContent = '✗ Erreur : ' + err.message;
                    status.style.color = '#dc3545';
                    fileInput.disabled = false;
                });
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.s3-file-input').forEach(initWidget);
    });

    /* Support dynamically added inline rows (Django admin "Ajouter un autre") */
    document.addEventListener('formset:added', function (e) {
        var row = e.target || (e.detail && e.detail.formset);
        if (!row) return;
        row.querySelectorAll('.s3-file-input').forEach(initWidget);
    });
})();
