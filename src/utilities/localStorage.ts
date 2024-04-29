export function getPropertyIdsFromLocalStorage(): string[] {
  let data = localStorage.getItem("opa_ids");

  if (data) {
    return Object.keys(JSON.parse(data).opa_ids);
  } else {
    return [];
  }
}
