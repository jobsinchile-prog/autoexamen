self.addEventListener('install',  () => self.skipWaiting());
self.addEventListener('activate', e  => e.waitUntil(clients.claim()));

self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SCHEDULE') programar(e.data.hora, e.data.titulo, e.data.cuerpo);
});

let t = null;
function programar(hora, titulo, cuerpo) {
  if (t) clearTimeout(t);
  function ms(h) {
    const a = new Date(), o = new Date();
    o.setHours(h, 0, 0, 0);
    if (o <= a) o.setDate(o.getDate() + 1);
    return o - a;
  }
  function loop() {
    self.registration.showNotification(titulo, { body: cuerpo, tag: 'autoexamen' });
    t = setTimeout(loop, 86400000);
  }
  t = setTimeout(loop, ms(hora));
}
