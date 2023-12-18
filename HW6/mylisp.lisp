;; I have to say that this is by far one of the most primitive and archaic languages known to man 
;; even assembly is better than this, because at least debugging is easier
;; It's like comparing a horse drawn carriage to a tesla
;; Plus the horses don't have horseshoes or reins (i.e. the lack of any functions outside of basic forms)
;; At least this is the last assignment. I wasted two days on this when it could have been done in python in five minutes.



;; Function to get last element of list 
(defun myLast (lst)
    (if (atom lst)
        ;true
        lst
        ;false
        (if (null (cdr lst))
        (car lst)
        (myLast (cdr lst))
        )
    )
)


;; count number of occurences in list
(defun myCount (x l)
  (if (null l)
      0
      (+ (if (eql x (car l)) 1 0)
         (myCount x (cdr l)))))


;; check if element is in list
(defun myMember (x l)
  (cond ((null l) nil)
        ((eql x (car l)) t)
        (t (myMember x (cdr l)))))


;; remove duplicate elements from a list
(defun myPurge2 (lst)
  (if (null lst)
      '()
      (let ((head (car lst))
            (tail (cdr lst)))
        (if (equal '(car lst) '(cdr lst))
            (myPurge2 '(cdr lst))
            (cons '(car lst) (myPurge2 '(cdr lst)))))))


; purge duplicate elements from the list
(defun myPurge (lst)
    (if (null lst) ;;check if list is null
        '()
        (if (atom lst) ; check if item is single atom, or is a list 
            ; yes
            lst
            ; no
            ; check if there is a duplicate of first element anywhere in list
            (if (contains-duplicate (car lst) (cdr lst))
                ; yes
                (myPurge (cdr lst))
                ; no
                ( cons (car lst) (myPurge (cdr lst)) )
            )
            ;no 
            ;lst
        )
    )
)
;; inputs: elem (a number), lst ( an evaluated list)
;; returns true (t) or false (nil)
(defun contains-duplicate (elem lst)
  (if (null lst)
      nil
      (if (equal elem (car lst))
        t
        (contains-duplicate elem (cdr lst))
      )
  )
)

; create list of all common elements of two lists
(defun myCommon (lst1 lst2)
    ; purge all duplicate elements from the result
    (myPurge
        ; check if lst1 is null
        (if (null lst1)
            '() ; yes
            ; no
            ; check if lst2 is null
            (if (null lst2)
                '() ;yes
                ; no
                ; iterate through list1, see if any duplicate elements in list2
                (if ( contains-duplicate (car lst1) lst2 )
                    ; yes
                    ( cons (car lst1) (myCommon (cdr lst1) lst2) )
                    ; no
                    (myCommon (cdr lst1) lst2)
                )
            ) 
        )
    )
)

;generate a list from X to Y, X <= Y
(defun myGen (X Y)
    (if (atom X) ; check if X is a single item and not a list
        ;yes
        (if (atom Y) ; check if X is a single item and not a list
            ;yes
            (if (> X Y) ; check if X > Y
                ;yes
                nil
                ;no
                (cons X (myGen (+ X 1) Y))
            )
            ;no
            nil
        )
        ;no
        nil
    )
)

; this only works if lst is a lst 
; if lst is an atom or f is not a function, it will crash
;call function func on every element of list lst
(defun myMap (func lst)
    (if (null lst)
        '()
        (cons (funcall func (car lst)) ; Apply function f to the first element
            (myMap func (cdr lst))
        )
    )
)

; call aggregate function on list
(defun myReduce (func lst)
    (if (null lst) ; check if list is empty
        (error "List is empty.")
        (if (null (cdr lst)) ; check if list is of length 1
            (error "List must have at least two elements.")
            (if (null (cdr (cdr lst))) ; check if list is of length 2
                ; yes
                (funcall func (car lst) (car (cdr lst))) ;return first element plus second element
                ; no
                (funcall func (car lst) (myReduce func (cdr lst))) ; return first element plus sum of everything after first element
            )
        )
    )
)



;; Call the functions with associated parameters
;;used for my own personal testing
;;(print 'myLast)
;;(print (myLast '(1 2 3 4 5)))
;;(print 'myCount)
;;(print (myCount '1 '(1 2 3 1 4 1 5)))
;;(print 'myMember)
;;(print (myMember '6 '(1 2 3 4 5)))
;;(print (myMember '4 '(1 2 3 4 5)))
;;(print 'myPurge)
;;(print (myPurge '(1 2)) )
;;(print (myPurge '(1 2 2 4 1 3 4)) )
;;(print (myPurge '(6 1 2 3 4 5 7 6)) )
;;(print (myPurge '1) )
;;(print 'myCommon)
;;(print (myCommon '(1 1 2 2 3 4 5) '(1 3 4 5 5 6 7 7)))
;;(print (myCommon '(2) '(1 3 5 7)))
;;(print 'myGen)
;;(print (myGen '2 '5))
;;(print (myGen '5 '5))
;;(print (myGen '5 '2))
;;(print 'myMap)
;;(print (myMap (lambda (x) (* x 2)) '(1 2)))
;;(print (myMap (lambda (x) (* x 2)) '(1 2 3)))
;;(print (myMap (lambda (x) (* x 2)) '(1)))
;;(print 'myReduce)
;;(print (myReduce(lambda (x y) (+ x y)) '(1 2)))
;;(print (myReduce (lambda (x y) (+ x y)) '(1 2 3 4 5)))



;;testing out commands
;;(   print ( cdr (cdr '(1 2)) )    )
;;(print (funcall (lambda (x) (* x 2)) 5))
;;(print (atom '(X Y)))
;;(print (atom 'X))
;;listp is the inverse of atom
;;(print (listp '(1 2 2 4 1 3 4)) )
;;(print (listp '2))
;;(setq x 10)
;;(print(x))
;;(print (car '(1 2 3)))
;;(print (contains-duplicate 3 '(1 2 3)))
;;(print (contains-duplicate (car '(1 2 3)) '(1 2 3)))
;;(print (myPurge '(1 2 3 1 2 4 5 4)))
;;(print (equal (car '(1 2 3)) (car '(1 2 3)) ))
;;(FRESH-LINE)

;;quit script
;; sbcl uses (exit), gcl uses (bye)
;;(exit)
;;(bye)