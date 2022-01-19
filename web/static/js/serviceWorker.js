// Bell Service Worker

PushManager.subscribe()
.then(sub => "Registered!")
.catch(err => "Failed.");


