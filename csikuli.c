#include <stdio.h>

#ifdef __linux
#include <X11/X.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#endif

int getNumberScreens() {
#ifdef __linux
	Display *display = XOpenDisplay(NULL);
	int n = XScreenCount(display);
	XCloseDisplay(display);
	return n;
#else
	printf("%s not implemented on this platform :(\n", __func__);
	return 1;
#endif
}

void capture(const int xx,const int yy,const int W, const int H, /*out*/ unsigned char * data) {
#ifdef __linux
	Display *display = XOpenDisplay(NULL);
	Window root = DefaultRootWindow(display);

	XImage *image = XGetImage(display,root, xx,yy, W,H, AllPlanes, ZPixmap);

	unsigned long red_mask   = image->red_mask;
	unsigned long green_mask = image->green_mask;
	unsigned long blue_mask  = image->blue_mask;
	int x, y;
	int ii = 0;
	for (y = 0; y < H; y++) {
		for (x = 0; x < W; x++) {
			unsigned long pixel = XGetPixel(image,x,y);
			unsigned char blue  = (pixel & blue_mask);
			unsigned char green = (pixel & green_mask) >> 8;
			unsigned char red   = (pixel & red_mask) >> 16;

			data[ii + 2] = blue;
			data[ii + 1] = green;
			data[ii + 0] = red;
			ii += 3;
		}
	}
	XDestroyImage(image);
	XDestroyWindow(display, root);
	XCloseDisplay(display);
#else
	printf("%s not implemented on this platform :(\n", __func__);
#endif
}
