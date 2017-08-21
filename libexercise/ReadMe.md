
刷题专用库
=============

collect.java
-------------

为什么要这个库？
因为我不会写Java.  

支持以下的东西：

1. Tuple<A, B> (可用于排序)
  
  ```
    e.g new Tuple<Double , Integer>(1.0, 2);
  ```
  

2. Range<T>

  ```
    e.g new Range(T begin, T end, step: T a->T b )
  ```

3. Seq

  ```
		.Map( (msg, item) -> ...)
		.Map( item -> ...)
		.Map( (int i, item) -> ...)

 		.argsort()
 		.argsort_by(item->...)
 		.argsort_by((i,item)->...)
 		.Join(spliter)
		
		.Index(Integer[] indices)   // change its self.
		.Indexed(Integer[] indices) // pure 

		.forEach( item-> ...)
		.forEachIndexed((int i ,item) -> ...)
		.forEachWithIndex((int i, seq<T>self) -> ...)
		.fromList(List<T>)
		.fromArray(T[] arr) 
  ```