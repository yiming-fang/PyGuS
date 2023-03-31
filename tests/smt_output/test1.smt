(define-fun max ((x Int) (y Int)) Int (ite (<= x y) y x))
(define-fun min ((x Int) (y Int)) Int (ite (<= x y) x y))
