// exported this function to be used in other files (PropertyMap.tsx)

export function toTitleCase(str: string | undefined | null) {
  if (str === null || str === undefined) return null;

  return str
    .toLowerCase()
    .split(' ')
    .map(function (word) {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(' ');
}
