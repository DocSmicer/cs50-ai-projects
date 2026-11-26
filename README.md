# Traffic: experimentation notes

## What I tried

I used a convolutional neural network and tested it on the full GTSRB data set (43 categories), with images resized to 30x30. Each run trained for 10 epochs on a random 60/40 train/test split.

My first version had two convolution layers (32 and then 64 filters, 3x3, ReLU), each followed by 2x2 max pooling. After that came a flatten layer, a hidden dense layer of 128 units, dropout of 0.5, and a softmax output layer of 43 units. It used the Adam optimizer and categorical cross-entropy. The first layer also rescales pixel values from 0-255 to 0-1.

For my second version I changed three things at once: I reduced the filters to 16 and 32, added a third convolution layer with 128 filters (without another pooling layer after it, because two poolings had already shrunk the image to about 5x5 pixels), and lowered the dropout from 0.5 to 0.2. The hidden layer stayed at 128 units.

| Version | Filters | Dropout | Training accuracy (epoch 10) | Test accuracy | Test loss | Time per step |
|---|---|---|---|---|---|---|
| First | 32, 64 | 0.5 | 0.9065 | 0.9810 | 0.0863 | about 32 ms |
| Second | 16, 32, 128 | 0.2 | 0.9876 | 0.9863 | 0.0520 | about 24 ms |

## What worked well

Both versions did well, but the second version was better on every measure I recorded. Its test accuracy was higher (0.9863 against 0.9810) and its test loss was lower (0.0520 against 0.0863). It also learned much faster at the start: after the first epoch its training accuracy was 0.5285, compared with 0.2835 for the first version. It ran faster per step as well, which is probably because it uses fewer filters in the first two layers.

## What didn't work as well, and what I noticed

The first version's training accuracy (0.9065) ended up lower than its test accuracy (0.9810). I think this is because dropout of 0.5 is applied only while training and is switched off when testing, so the training numbers look worse than the model really is. In the second version, with dropout of 0.2, training accuracy (0.9876) and test accuracy (0.9863) were almost equal, so I saw no sign of overfitting in either version.

The main weakness of my experiments is that I changed three things at once, so I cannot say which change caused the improvement. It may have been the lower dropout, the extra convolution layer, or both. I also ran each version only once, and because the train/test split is random, a difference of about half a percentage point in test accuracy may partly be noise. With more time I would change one setting at a time and repeat each run a few times, to see what actually made the difference.
