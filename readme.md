# Pi Pico Client & Server

## Getting Started - flashing firmware

- Plug your micro USB cable into the Pi Pico
- Hold down the BOOTSEL button on the Pico
- Insert the other end of the cable into your computer (keep holding button)

You should now have the Pico mounted to your computer. At this point you can release the button.

Drag over the `firmware*.uf2` file to the Pico and it should begin flashing on it's own.
When it reboots, you will see some different files.

### _Repeat the steps above for all Picos you have_

---

## Copying the client & server code

Due to the Pico's acting in pairs, there are 2 folders in this repo.

- Simply plug in each device and alternatively copy the contents (not the folder itself) of the client & server folders over, like this:

```ascii
├── PI A (Client)/
│   ├── lib/
│   └── code.py
└── Pi B (Server)/
    ├── lib/
    └── code.py
```

- Power off both devices, plug in the ethernet cable between them and power back on.

The LED status lights on the ethernet port should be blinking indicating activity between them. Congrats!

## _Note_

If you need to change the html document, you can edit the variable `html_string` in server/code.py
