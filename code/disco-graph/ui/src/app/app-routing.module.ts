import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './components/util/page-not-found/page-not-found.component';

const routes: Routes = [
  {path: '', redirectTo: '/search', pathMatch: 'full'},
  {path: '**', component: PageNotFoundComponent}
]

@NgModule({
  imports: [RouterModule.forRoot(routes,
    {enableTracing: true})], // TODO: Use only for debugging
  exports: [RouterModule]
})
export class AppRoutingModule { }
