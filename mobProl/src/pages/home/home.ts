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
    //this.programCodeString = "main() {var int a = 0; print(\"Hola\")}";
    this.programCodeString = "var int a; var decim c; var int d; func int uno(int a, decim b, int c){var int z; a = c + 34;} main(){var decim b; var int f; var decim g; var bool myBool; myBool = 1 == 2; g = 1.0; f = 2; b = f+g*(4+5/2); a = 6;}";
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
            + this.programCodeString.replace(/\n/g, "")
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
    
    console.log("normal response is: " + response);
    let jsonResponse = JSON.parse(response.json().data);
    console.log("Your json is: ")
    console.log(jsonResponse);

    for(var i = 0; i < jsonResponse.length; i++) {
      var obj = jsonResponse[i];
      let tempQuad = [];
  
      tempQuad.push(obj.arg1);
      tempQuad.push(obj.arg2);
      tempQuad.push(obj.arg3);
      tempQuad.push(obj.arg4);

      this.quadruples.push(tempQuad);
    }

    console.log("Received quadruples to execute:");
    
    console.log(this.quadruples);
  }

  /**
   * Uses quadruples to run commands, showing output on screen
   */
  async run() {
    console.log("debug: Running program...");
    const modal = this.modalCtrl.create(OutputPage, {programName: this.programName, quadruples: this.quadruples});

    modal.onWillDismiss(() => {
      this.quadruples = [];
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
