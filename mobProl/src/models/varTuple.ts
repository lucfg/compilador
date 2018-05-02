export class varTuple {
    //value: any;
    constructor(public value: any) {
        this.value = value;
    }
  }
  
  interface HashTable<T> {
    [key: number]: T;
  }