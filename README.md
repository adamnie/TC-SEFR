# TC-SEFR
Self-embedding fragile watermarking based on DCT and fast fractal coding.

An application I made with [Antoni Grzanka](https://github.com/anteq).
It makes use of the Fractal coding and DCT to make 3 watermarks for an image,
and then embed them into the image itself (last 2 bits of each pixel).

With those watermarks it is possible to check whether the image was tampered or
even to reconstruct it if damaged.

It works only for grayscale images, though it could easily be extended into RGB.
