import sys
import json
import struct

class Message(object):

    def __init__(self, action, from_id, to_id, value, type="text/json", encoding="utf-8",):
        self._action = action
        self._from_id = from_id
        self._to_id = to_id
        self._value = value
        self._content_type = type
        self._content_encoding = encoding
        self._content = self._get_content()
        self.content_bytes = self._json_encode(self._content, self._content_encoding)

        self.message = self._get_message()

    def _get_message(self):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": self._content_type,
            "content-encoding": self._content_encoding,
            "content-length": len(self.content_bytes),
        }


        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + self.content_bytes
        return message

    def _get_content(self):
        if self._action == "transmit":
            return dict(
                action=self._action,
                from_id=self._from_id,
                to_id=self._to_id,
                value=self._value
            )
        elif self._action == "login" or self._action == "out":
            return dict(action=self._action, from_id=self._from_id)
        elif self._action == "search":
            return dict(action=self._action, value=self._value)
        else:
            return bytes(self._action + self._value, encoding="utf-8")

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

