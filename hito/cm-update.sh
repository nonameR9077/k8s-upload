#!/bin/sh
kubectl delete cm -n hito cm-hito-update-checker && kubectl create cm -n hito cm-hito-update-checker --from-file python/old/hito-update-checker.py
kubectl delete cm -n hito cm-e-hen-update-checker && kubectl create cm -n hito cm-e-hen-update-checker \
	--from-file python/e-hen/main.py \
	--from-file python/e-hen/crawler.py \
	--from-file python/e-hen/utils.py \
	--from-file python/e-hen/constants.py
