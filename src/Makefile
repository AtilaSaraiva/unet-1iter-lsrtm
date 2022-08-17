$(MODELDIR)/spaceUnet.pt: space_domain_train.py tile_dataset.py trainUnetClass.py unet.py
	python space_domain_train.py

:$(DATADIR)/filtered_space_domain_image.h5: space_domain_inference.py
	python space_domain_inference.py
