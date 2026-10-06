'use strict';
const videos = [...document.querySelectorAll('video')];
for (const video of videos) {
  video.addEventListener('play', () => videos.forEach(other => { if (other !== video) other.pause(); }));
  video.addEventListener('error', () => { video.closest('.screen').querySelector('.video-note').hidden = false; });
}
