// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '/static/css/styles.css'
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});



// notificaciones push
importScripts('https://www.gstatic.com/firebasejs/4.12.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/4.12.0/firebase-messaging.js');

var firebaseConfig = {
    apiKey: "AIzaSyDv-jcKih2n0IR-OWuDPRqj6nPG9y58kFo",
    authDomain: "serviciosya-6222e.firebaseapp.com",
    projectId: "serviciosya-6222e",
    storageBucket: "serviciosya-6222e.appspot.com",
    messagingSenderId: "742882808683",
    appId: "1:742882808683:web:7c2ae10b51484c7ef0322e"
  };

  // Initialize Firebase
firebase.initializeApp(firebaseConfig);

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
    
    let title = payload.notification.title;

    let options = {
        body:payload.notification.body ,
        icon:'/static/assets/img/logos/google.svg',
        data:{
            time: new Date(Date.now()).toString(),
            click_action: payload.notification.click_action
        }
    }
    

    self.registration.showNotification(title, options);
})
self.addEventListener('notificationclick', function(event) {
    let action_click=event.notification.click_action;
    event.notification.close()

    event.waitUntil(
        clients.openWindow(action_click)
    );
});





/*despues de function(payload).......{self.registration.showNotification(payload.data.title,{'body':payload.data.body,'icon':payload.data.icon,'click_action':payload.data.click_action,'image':payload.data.image});self.addEventListener('notificationclick',function(event){let url=payload.data.click_action;event.notification.close();event.waitUntil(clients.matchAll({type:'window'}).then(windowClients=>{for(var i=0;i<windowClients.length;i++){var client=windowClients[i];if(client.url===url&&'focus'in client){return client.focus();}}
if(clients.openWindow){return clients.openWindow(url);}}));});});*/