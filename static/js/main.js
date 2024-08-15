function dismissToast() {
  const toasts = document.querySelectorAll(".toast");
  toasts.forEach((toast) => toast.remove());
}
setTimeout(dismissToast, 3000);
