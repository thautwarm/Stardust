// 刷Java题专用
/*
	Tuple
	Range
	Seq 
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


*/

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.BiConsumer;
import java.util.function.BiFunction;

public class Algorithm {

	public static class tup<A,B>{
		A a;
		B b;
		tup(A a, B b){
			this.a = a;
			this.b = b;
		}
	}
	
	public static class Tuple<A,B> implements Comparable<Tuple<A,B>>, Comparator<Tuple<A,B>>{
		tup<A,B> t;
		public Tuple(){};
		public Tuple(A a, B b){
			t = new tup<A,B>(a,b);
		}
		@Override
		public int compareTo(Tuple<A, B> o) {
			return new Double((double) t.a).compareTo(new Double((double) o.t.a));
		}
		@Override
		public int compare(Tuple<A, B> left, Tuple<A, B> right) {
			// TODO Auto-generated method stub
			return Double.compare( (double)left.t.a, (double) right.t.a );
		}
		


		
	}
	public static class Range<T> {
	    private T low;
	    private T high;
	    private Function<T, T> iter_action;

	    public Range(T low, T high, Function<T, T> iter_action){
	        this.low         = low;
	        this.high 		 = high;
	        this.iter_action = iter_action;
	    }

	    public void forEach(Consumer<T> f){
	    	while (!low.equals(high) ){
	    		f.accept(low);
	    		low = iter_action.apply(low);
	    	}
	    }
	}

	
	@SuppressWarnings("serial")
	public static class Seq<T> extends ArrayList<T>{
		
		Seq(int capi){
			super(capi);
		}	
		
		public <R> Seq<R> Do( Function<Seq<T>,Seq<R>> f){	
			return f.apply(this);
				
		}
		
		public  Integer[] argsort(){
			int size = this.size();
			Integer[] ret= new Integer[size];
			Tuple<T, Integer> comp = new Tuple<T, Integer>();
			Seq<Tuple<T, Integer>> idx_arr =  this.MapIndexed((i,item)->  new Tuple<T, Integer>(item, i) );
			idx_arr.sort(comp);
			return idx_arr.Map(tup->tup.t.b).toArray(ret);			    
	 
	    }
		
		public <R> Integer[] argsort_by(Function<T,R> f){
			return this.Map(f).argsort();
	    }
		public <I, R> Integer[] argsort_by(BiFunction<I, T, R> f, I msg){
			return this.Map(f, msg).argsort(); 
	    }	
		public <R> Seq<R> Map(Function<T, R> f){
			int size = this.size();
			Seq<R> newlist = new Seq<R>(size);
			new Range<Integer>(0, size, i->++i).forEach(i->newlist.add(f.apply(this.get(i))));
			return newlist;
		}
		public <R> Seq<R> MapIndexed(BiFunction<Integer, T, R> f){
			int size = this.size();
			Seq<R> newlist = new Seq<R>(size);
			new Range<Integer>(0, size, i->++i).forEach(i->newlist.add(f.apply(i,this.get(i))));
			return newlist;
		}
		public <I, R> Seq<R> Map(BiFunction<I, T, R> f, I msg){
			int size = this.size();
			Seq<R> newlist = new Seq<R>(size);
			new Range<Integer>(0, size, i->++i).forEach(i->newlist.add(f.apply(msg, this.get(i))));
			return newlist;
		}
		public  Double Mean( Function<T, Double> f){		
			Double sum = 0.0;
			for(double item :this.Map(f)) sum+=item;
			return sum/this.size();
		}

		public Seq<Double> Diff(){		
			Seq<Double> newlist = new Seq<Double>(this.size()-1);
			new Range<Integer>(1, this.size(), i->++i).forEach( i-> newlist.add( (Double)this.get(i)-(Double)this.get(i-1) ));
			return newlist;
		}
		public Seq<T>  Indexed(Integer[] indices){
			int size= indices.length;
			Seq<T> newlist = new Seq<T>(size);
			new Range<Integer>(0, size, i->++i).forEach( i -> newlist.add(this.get(indices[i])));
			return newlist;
		}
		
		@SuppressWarnings("unchecked")
		public Seq<T>  Index(Integer[] indices){
			int size= indices.length;		
			Object[] swap = new Object[size];
			new Range<Integer>(0, size, i->++i).forEach( i ->swap[i] = this.get(indices[i]));
			for(int i = 0; i < size; ++i)
				this.set(i, (T) swap[i]);
			return this;
		}
		
		
		public Seq<T> forEachIndexed(BiConsumer<Integer, T> f){
			new Range<Integer>(0, this.size(), i->++i).forEach( i->f.accept(i, this.get(i)));
			return this;
		}
		public Seq<T> forEachWithIndex(BiConsumer<Integer, Seq<T>> f){
			new Range<Integer>(0, this.size(), i->++i).forEach(i->f.accept(i, this));
			return this;
		}
		public String Join(String spliter){
			return String.join(spliter, this.Map(i->(String)i ));
		}
		
		public void reload(int n){
			new Range<Integer>(n, this.size(), i->++i).forEach(i->this.set(i, this.get(i%n)));
		}
		
		public void reload(int n, int stop){
			new Range<Integer>(n, stop, i->++i).forEach(i->this.set(i, this.get(i%n)));
		}
		public void load(int begin , Seq<T> toload){
			new Range<Integer>(0, toload.size(), i->++i).forEach(i->this.set(i+begin, toload.get(i)));
		}
		public void load(int begin ,T[] toload){
			new Range<Integer>(0, toload.length, i->++i).forEach(i->this.set(i+begin, toload[i]));
		}
		public void loadBy(int begin , Function<T, T>  ftoload){
			new Range<Integer>(begin, this.size(), i->++i).forEach(i->this.set(i, ftoload.apply(this.get(i))));
		}
		public void loadBy(int begin , int stop, Function<T, T>  ftoload){
			new Range<Integer>(begin, stop, i->++i).forEach(i->this.set(i, ftoload.apply(this.get(i))));
		}


		
		public static <T> Seq<T> fromList( List<T> arrlist ){
			Seq<T> seq = new Seq<T>(arrlist.size());
			arrlist.forEach(item -> seq.add(item));
			return seq;
		}
		public static <T> Seq<T> fromArray( T[] arr ){
			Seq<T> seq = new Seq<T>(arr.length);
			for(T item : arr ) seq.add(item); 
			return seq;
		}
		
	}
}
