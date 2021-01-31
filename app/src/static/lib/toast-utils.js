
let _toast_utils_global_obj = undefined;

const TOAST_DOING = {
  style: {
    main: {
      background: "#1826a5",
      color: "#fff"
    }
  },
  settings: {
    duration: 2000
  }
};

const TOAST_OK = {
  style: {
    main: {
      background: "#0e7c20",
      color: "#fff"
    }
  },
  settings: {
    duration: 5000
  }
};

const TOAST_ERROR = {
  style: {
    main: {
      background: "#a01616",
      color: "#fff"
    }
  },
  settings: {
    duration: 5000
  }
};

function toast(msg, color) {
  if (_toast_utils_global_obj) {
    _toast_utils_global_obj.destroy();
  }

  _toast_utils_global_obj = iqwerty.toast.Toast(msg, color);
}
