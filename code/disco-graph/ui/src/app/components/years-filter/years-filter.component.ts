import { CdkAriaLive } from '@angular/cdk/a11y';
import { ChangeDetectorRef, Component, EventEmitter, Output } from '@angular/core';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'app-years-filter',
  templateUrl: './years-filter.component.html',
  styleUrls: ['./years-filter.component.scss']
})
export class YearsFilterComponent {

  @Output() filterChangedEvent = new EventEmitter();

  ERROR_MSG: string = "Currently unable to set the filter.";
  gotErrorResponse: boolean = false;

  constructor (
    private filterService: FilterService,
    private cd: ChangeDetectorRef,
  ) {}

  currentYear: number = new Date().getFullYear();
  firstYear: number = 1975;
  minValue: number = this.firstYear.valueOf();
  maxValue: number = this.currentYear.valueOf();
  cachedPreviousMinValue = this.firstYear.valueOf();
  cachedPreviousMaxValue = this.currentYear.valueOf();


  formatLabel(value: number, baseYear:number = 1975): string{
    if (baseYear >= value){
      return `<${baseYear}`;
    }
    return String(value);
  }

  valueChanged(){
    if(this.cachedPreviousMinValue !== this.minValue 
      || this.cachedPreviousMaxValue !== this.maxValue){
        this.cachedPreviousMinValue = this.minValue.valueOf();
        this.cachedPreviousMaxValue = this.maxValue.valueOf();
        this.filterChangedEvent.emit();

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
