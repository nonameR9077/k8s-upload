#!/bin/sh
kubectl delete cm -n macro cm-bananamall && kubectl create cm -n macro cm-bananamall --from-file python/macro-bananamall.py
kubectl delete cm -n macro cm-dingdong && kubectl create cm -n macro cm-dingdong --from-file python/macro-dingdong.py
kubectl delete cm -n macro cm-domaedoll && kubectl create cm -n macro cm-domaedoll --from-file python/macro-domaedoll.py
kubectl delete cm -n macro cm-oname && kubectl create cm -n macro cm-oname --from-file python/macro-oname.py
kubectl delete cm -n macro cm-showdang && kubectl create cm -n macro cm-showdang --from-file python/macro-showdang.py
kubectl delete cm -n macro cm-sofrano && kubectl create cm -n macro cm-sofrano --from-file python/macro-sofrano.py
