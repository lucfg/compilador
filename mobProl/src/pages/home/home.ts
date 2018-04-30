import { Component, ViewChild, ElementRef } from '@angular/core';
import { Http } from '@angular/http';
import { NavController } from 'ionic-angular';
import { map } from 'rxjs/operators';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  programName: string;
  programCodeString: string;
  fullCodeString: string;

  // Interface
  @ViewChild('myInput') myInput: ElementRef;
  keyChar = '{';
  keyChar2 = '}';

  constructor(
        public navCtrl: NavController,
        private http: Http,
    ) {
    this.programName = "myProgram"
    this.programCodeString = "main() {}";
  }

  ionViewDidLoad(){
    this.resizeTextArea();
  }

  async compileAndRun() {
    console.log("debug: Compiling code...");
    let data = {
        code: "test code"
    };

    this.http.post('http://localhost:8080/compile', data).pipe(
        map(res => res.json())
    ).subscribe(response => {
      console.log("Response quadruples are:");  
      console.log(response.quadruples);
    });
  }

  /**
   * Sends code to python and receives cuadruples to execute
   */
  compile() {
    //TODO: run python code
  }

  run(quadruples) {
    //TODO: receive and execute quadruples
  }

  

  /**
   * Makes sure that all code is visible within the text-area
   */
  resizeTextArea() {
    let minHeight = 20;
    let height = this.myInput.nativeElement.scrollHeight;
    if (height < minHeight) {
      height = minHeight;
    }

    this.myInput.nativeElement.style.height = height + 'px';
  }
}
