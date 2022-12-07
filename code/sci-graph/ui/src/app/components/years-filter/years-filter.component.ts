import { CdkAriaLive } from '@angular/cdk/a11y';
import { ChangeDetectorRef, Component, EventEmitter } from '@angular/core';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'app-years-filter',
  templateUrl: './years-filter.component.html',
  styleUrls: ['./years-filter.component.scss']
})
export class YearsFilterComponent {

  ERROR_MSG: string = "Currently unable to set the filter.";
  gotErrorResponse: boolean = false;

  constructor (
    private filterService: FilterService,
    private cd: ChangeDetectorRef,
  ) {}

  currentYear: number = new Date().getFullYear();
  firstYear: number = 1900;
  minValue: number = 1900;
  maxValue: number = this.currentYear.valueOf();
  cachedPreviousMinValue = 1900;
  cachedPreviousMaxValue = this.currentYear.valueOf();


  formatLabel(value: number): string{
    return String(value);
  }

  valueChanged(){
    if(this.cachedPreviousMinValue !== this.minValue 
      || this.cachedPreviousMaxValue !== this.maxValue){
        this.cachedPreviousMinValue = this.minValue.valueOf();
        this.cachedPreviousMaxValue = this.maxValue.valueOf();

        let responseHandler = {
          error: (e: any) => {
            this.gotErrorResponse = true;
            console.log(e);
            this.cd.detectChanges()
          },
          complete: () => {
            this.gotErrorResponse = false;
            this.cd.detectChanges()
          },
        };

        if(this.minValue === this.firstYear && this.maxValue === this.currentYear){
          this.filterService
          .deleteYearsFilter()
          .subscribe(responseHandler)
          return;
        }
        this.filterService
        .setYearsFilter(this.minValue, this.maxValue)
        .subscribe(responseHandler);
    }
  }

}
