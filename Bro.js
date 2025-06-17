(function() {
  // Make all buttons run away on hover
  document.querySelectorAll('button').forEach(button => {
    button.style.position = 'relative';
    button.addEventListener('mouseenter', () => {
      button.style.left = Math.floor(Math.random() * 200 - 100) + 'px';
      button.style.top = Math.floor(Math.random() * 200 - 100) + 'px';
    });
  });

  // Slowly rotate all text on the page
  let angle = 0;
  setInterval(() => {
    angle = (angle + 1) % 360;
    document.body.style.transform = `rotate(${angle}deg) translate(${Math.random()*10-5}px, ${Math.random()*10-5}px)`;
  }, 50);

  // Invert colors every 3 seconds
  let inverted = false;
  setInterval(() => {
    document.body.style.filter = inverted ? "invert(0)" : "invert(1)";
    inverted = !inverted;
  }, 3000);

  // Replace all images every 2 seconds with a meme
  const memeURL = "https://i.imgur.com/1cX0rLa.jpg"; // Funny meme image link
  setInterval(() => {
    document.querySelectorAll('img').forEach(img => {
      img.src = memeURL;
    });
  }, 2000);

  // Shake page content like earthquake
  setInterval(() => {
    const x = Math.random() * 10 - 5;
    const y = Math.random() * 10 - 5;
    document.body.style.transform += ` translate(${x}px, ${y}px)`;
  }, 100);

  // Random virus alert popups every 6 to 12 seconds
  const alerts = [
    "Warning! Virus detected!",
    "System error! Virus found!",
    "Your PC has virus!",
    "Critical virus detected!",
    "Virus is spreading!",
    "Alert! Formatting Windows!",
    "System unstable. Restart required!",
    "Your all files are deleted!"
  ];

  function randomAlert() {
    const msg = alerts[Math.floor(Math.random() * alerts.length)];
    alert(msg);
    const delay = Math.random() * 6000 + 6000; // 6-12 seconds
    setTimeout(randomAlert, delay);
  }

  setTimeout(randomAlert, 8000); // Start alerts after 8 seconds
})();
