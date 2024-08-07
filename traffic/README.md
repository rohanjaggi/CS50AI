Initially, I only had one hidden layer and one convolutional and
pooling layer. However, the results were not great as the accuracy
was only 0.5703.

Hence, I decided to add a second convolutional and pooling layer
which boosted the accuracy to around 0.9155, which marked a step in
the right direction. 

Furthering on, I added another hidden layer at the end, but the jump
in accuracy was not very profound, with accuracy only jumping to
0.9176. With this information, I added 2 more hidden layers, making
it 4 hidden layers, and there was a bigger jump in the accuracy as
it moved up to 0.9619, which ended up being the highest value I got.

I tried to improve the model by adding a third convolutional and
pooling layer, but this did not seem to help the accuracy, as it
fell back down to 0.9160. Removing that layer, but adding a 5th
hidden layer boosted the accuracy back up to 0.9588, but crucially,
it was still lower than the accuracy when there were only 4 hidden
layers.

This goes to show that more is never better. In order to get the
highest accuracy, there is a need to hit the "sweet-spot", which in
my case, turned out to be when there were 2 convolutional and
pooling layers, followed by 4 hidden layers in the neural network.
