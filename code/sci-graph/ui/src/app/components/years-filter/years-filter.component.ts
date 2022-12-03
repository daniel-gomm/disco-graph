import { Component, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-years-filter',
  templateUrl: './years-filter.component.html',
  styleUrls: ['./years-filter.component.scss']
})
export class YearsFilterComponent {

  currentYear: number = new Date().getFullYear();
  firstYear: number = 1900;
  minValue: number = 1900;
  maxValue: number = this.currentYear;


  formatLabel(value: number): string{
    return String(value);
  }

  valueChanged(){
    console.log('Value changed')
  }

}
