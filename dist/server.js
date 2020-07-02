"use strict";

var _app = _interopRequireDefault(require("./app"));

var _config = _interopRequireDefault(require("./config"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var PORT = _config["default"].PORT;

_app["default"].listen(PORT, function () {
  return console.log("Server started and listening on PORT ".concat(PORT));
});