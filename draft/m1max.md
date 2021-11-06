
Title: Tensorflow on an Apple MacbookPro M1 Max
Date: 2021-11-21
Modified: 2021-11-21
Category: Deep Learning
Tags: datascience, m1, apple, tensorflow
Slug: m1max
Authors: Brian Roepke
Summary: A comparison of training a neural network on a first gen M1 Mac vs. the monster M1 Max with 32 core GPU.
Header_Cover: images/computer.jpg
Og_Image: images/computer.jpg
Twitter_Image: images/computer.jpg

## The 2021 Macbook Pro M1 Max


## Installing the Latest Apple Silicon Tensorflow

https://developer.apple.com/metal/tensorflow-plugin/ 


```
Epoch 1/10
702/702 [==============================] - 41s 59ms/step - loss: 0.6462 - accuracy: 0.6129 - val_loss: 0.5476 - val_accuracy: 0.7166
Epoch 2/10
702/702 [==============================] - 39s 55ms/step - loss: 0.5105 - accuracy: 0.7497 - val_loss: 0.5180 - val_accuracy: 0.7447
Epoch 3/10
702/702 [==============================] - 40s 56ms/step - loss: 0.4704 - accuracy: 0.7751 - val_loss: 0.5368 - val_accuracy: 0.7327
Epoch 4/10
702/702 [==============================] - 37s 53ms/step - loss: 0.4154 - accuracy: 0.8047 - val_loss: 0.4735 - val_accuracy: 0.7856
Epoch 5/10
702/702 [==============================] - 37s 53ms/step - loss: 0.3766 - accuracy: 0.8288 - val_loss: 0.4748 - val_accuracy: 0.7804
Epoch 6/10
702/702 [==============================] - 38s 55ms/step - loss: 0.3245 - accuracy: 0.8573 - val_loss: 0.4900 - val_accuracy: 0.7896
Epoch 7/10
702/702 [==============================] - 37s 52ms/step - loss: 0.2686 - accuracy: 0.8879 - val_loss: 0.5298 - val_accuracy: 0.7828
Epoch 8/10
702/702 [==============================] - 38s 53ms/step - loss: 0.1996 - accuracy: 0.9210 - val_loss: 0.5467 - val_accuracy: 0.7868
Epoch 9/10
702/702 [==============================] - 37s 53ms/step - loss: 0.1512 - accuracy: 0.9440 - val_loss: 0.6506 - val_accuracy: 0.7860
Epoch 10/10
702/702 [==============================] - 37s 53ms/step - loss: 0.1014 - accuracy: 0.9628 - val_loss: 0.7223 - val_accuracy: 0.7820
```












```
Epoch 1/10
2021-11-05 10:33:15.456260: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:112] Plugin optimizer for device_type GPU is enabled.
702/702 [==============================] - ETA: 0s - loss: 0.6174 - accuracy: 0.64862021-11-05 10:33:26.647448: I tensorflow/core/grappler/optimizers/custom_graph_optimizer_registry.cc:112] Plugin optimizer for device_type GPU is enabled.
702/702 [==============================] - 12s 16ms/step - loss: 0.6174 - accuracy: 0.6486 - val_loss: 0.5341 - val_accuracy: 0.7351
Epoch 2/10
702/702 [==============================] - 11s 16ms/step - loss: 0.5040 - accuracy: 0.7541 - val_loss: 0.5037 - val_accuracy: 0.7539
Epoch 3/10
702/702 [==============================] - 11s 16ms/step - loss: 0.4468 - accuracy: 0.7881 - val_loss: 0.4743 - val_accuracy: 0.7687
Epoch 4/10
702/702 [==============================] - 11s 16ms/step - loss: 0.3987 - accuracy: 0.8176 - val_loss: 0.4686 - val_accuracy: 0.7788
Epoch 5/10
702/702 [==============================] - 11s 16ms/step - loss: 0.3499 - accuracy: 0.8434 - val_loss: 0.4670 - val_accuracy: 0.7828
Epoch 6/10
702/702 [==============================] - 11s 16ms/step - loss: 0.2933 - accuracy: 0.8715 - val_loss: 0.4893 - val_accuracy: 0.7848
Epoch 7/10
702/702 [==============================] - 11s 16ms/step - loss: 0.2361 - accuracy: 0.9009 - val_loss: 0.5265 - val_accuracy: 0.7836
Epoch 8/10
702/702 [==============================] - 11s 16ms/step - loss: 0.1759 - accuracy: 0.9302 - val_loss: 0.5924 - val_accuracy: 0.7852
Epoch 9/10
702/702 [==============================] - 11s 16ms/step - loss: 0.1116 - accuracy: 0.9587 - val_loss: 0.6581 - val_accuracy: 0.7804
Epoch 10/10
702/702 [==============================] - 11s 16ms/step - loss: 0.0705 - accuracy: 0.9771 - val_loss: 0.7531 - val_accuracy: 0.7912
```




## References

https://soorajsknair.medium.com/how-and-why-exploratory-data-analysis-eda-used-in-python-data-analysis-db451394eb7f