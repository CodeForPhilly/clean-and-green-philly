module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description:
        'disallow specific `text-` size classes, enforce `heading-*` and `body-*`',
      category: 'Stylistic Issues',
      recommended: false,
    },
    fixable: null,
    schema: [],
  },
  create: function (context) {
    return {
      JSXAttribute(node) {
        if (node.name.name !== 'className') {
          return;
        }

        // Generates list of text-xs to text-xl, text-2xl to text-9xl
        const disallowedTailwindTextSizeClasses = [
          ...['xs', 'sm', 'md', 'lg', 'xl'],
          ...Array.from({ length: 8 }, (_, i) => `${i + 2}xl`),
        ].map((size) => `text-${size}`);

        const containsDisallowedClass = (value) => {
          return disallowedTailwindTextSizeClasses.some((disallowedClass) =>
            value.includes(disallowedClass)
          );
        };

        if (node.value.type === 'Literal' || node.value.type === 'JSXText') {
          const value = node.value.value;
          if (containsDisallowedClass(value)) {
            context.report({
              node,
              message:
                'Use `heading-*` or `body-*` classes instead of specific `text-` size classes.',
            });
          }
        } else if (node.value.type === 'TemplateLiteral') {
          const quasis = node.value.quasis.map((q) => q.value.cooked);
          const templateValue = quasis.join('');
          if (containsDisallowedClass(templateValue)) {
            context.report({
              node,
              message:
                'Use `heading-*` or `body-*` classes instead of specific `text-` size classes in template literals.',
            });
          }
        }
      },
    };
  },
};
