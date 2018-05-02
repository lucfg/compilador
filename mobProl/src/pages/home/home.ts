import { Component, ViewChild, ElementRef } from '@angular/core';
import { Http } from '@angular/http';
import { NavController, ModalController } from 'ionic-angular';
import { map } from 'rxjs/operators';
import { OutputPage } from '../output/output';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
  programName: string;
  programCodeString: string;

  quadruples = [];

  // Interface
  @ViewChild('myInput') myInput: ElementRef;
  keyChar = '{';
  keyChar2 = '}';

  constructor(
        public navCtrl: NavController,
        public modalCtrl: ModalController,
        private http: Http,
    ) {
    this.programName = "myProgram"
    this.programCodeString = "main() {var int a = 0; print(\"Hola\")}";
  }

  ionViewDidLoad(){
    this.resizeTextArea();
  }

  async compileAndRun() {
    await this.compile();
    await this.run();
  }

  /**
   * Sends code to python and receives cuadruples to execute
   */
  async compile() {
    console.log("Compiling code...");
    let data = {
        code: "program " + this.programName + "{ "
            + this.programCodeString
            + " }"
    };

    var response;
    try {
      response = await this.http.post('http://localhost:8080/compile', data).toPromise();  
    } catch (err) {
      console.log("Error while trying to access the server: " + err.message);
    }

    if (!response) {
      return;
    }
    
    let jsonResponse = response.json();
    this.quadruples = jsonResponse.quadruples;

    console.log("Received quadruples to execute:");
    console.log(this.quadruples);
  }

  /**
   * Uses quadruples to run commands, showing output on screen
   */
  async run() {
    console.log("debug: Running program...");
    const modal = this.modalCtrl.create(OutputPage, {quadruples: this.quadruples});

    modal.onWillDismiss(() => {
      // No interface updates needed?
    });

    modal.present();
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
