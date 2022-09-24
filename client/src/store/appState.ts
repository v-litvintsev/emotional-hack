import { makeAutoObservable } from "mobx";

class AppState {
  constructor() {
    makeAutoObservable(this);
  }
}

export default new AppState();
