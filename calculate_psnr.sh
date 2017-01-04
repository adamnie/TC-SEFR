sudo apt install imagemagick

compare -metric PSNR pepper.pgm pepper_watermarked.pgm  diff.pgm >> diff.txt
