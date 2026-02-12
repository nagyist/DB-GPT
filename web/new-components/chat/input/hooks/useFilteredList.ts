import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

export interface UseFilteredListOptions<T> {
  items: T[] | ((query: string) => Promise<T[]> | T[]);
  key: (item: T | undefined) => string;
  filterKeys: (keyof T)[];
  onSelect: (item: T | undefined) => void;
  debounceMs?: number;
}

export interface UseFilteredListReturn<T> {
  flat: T[];
  active: string | null;
  setActive: (key: string | null) => void;
  onInput: (query: string) => void;
  onKeyDown: (event: React.KeyboardEvent) => boolean;
  reset: () => void;
  query: string;
  loading: boolean;
}

export function useFilteredList<T>(options: UseFilteredListOptions<T>): UseFilteredListReturn<T> {
  const { items, key, filterKeys, onSelect, debounceMs = 150 } = options;

  const [query, setQuery] = useState('');
  const [allItems, setAllItems] = useState<T[]>([]);
  const [active, setActive] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  const fetchItems = useCallback(
    async (searchQuery: string) => {
      setLoading(true);
      try {
        if (typeof items === 'function') {
          const result = await items(searchQuery);
          setAllItems(result);
        } else {
          setAllItems(items);
        }
      } catch (error) {
        console.error('Error fetching items:', error);
        setAllItems([]);
      } finally {
        setLoading(false);
      }
    },
    [items],
  );

  const flat = useMemo(() => {
    if (!query) return allItems;

    const lowerQuery = query.toLowerCase();
    return allItems.filter(item => {
      return filterKeys.some(filterKey => {
        const value = item[filterKey];
        if (typeof value === 'string') {
          return value.toLowerCase().includes(lowerQuery);
        }
        return false;
      });
    });
  }, [allItems, query, filterKeys]);

  useEffect(() => {
    if (flat.length > 0 && !active) {
      setActive(key(flat[0]));
    } else if (flat.length === 0) {
      setActive(null);
    }
  }, [flat, active, key]);

  const onInput = useCallback(
    (newQuery: string) => {
      setQuery(newQuery);

      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }

      debounceRef.current = setTimeout(() => {
        fetchItems(newQuery);
      }, debounceMs);
    },
    [fetchItems, debounceMs],
  );

  const onKeyDown = useCallback(
    (event: React.KeyboardEvent): boolean => {
      if (flat.length === 0) return false;

      const currentIndex = flat.findIndex(item => key(item) === active);

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault();
          const nextIndex = currentIndex < flat.length - 1 ? currentIndex + 1 : 0;
          setActive(key(flat[nextIndex]));
          return true;

        case 'ArrowUp':
          event.preventDefault();
          const prevIndex = currentIndex > 0 ? currentIndex - 1 : flat.length - 1;
          setActive(key(flat[prevIndex]));
          return true;

        case 'Enter':
        case 'Tab':
          event.preventDefault();
          const selectedItem = flat.find(item => key(item) === active) ?? flat[0];
          onSelect(selectedItem);
          return true;

        case 'Escape':
          event.preventDefault();
          setActive(null);
          return true;

        default:
          return false;
      }
    },
    [flat, active, key, onSelect],
  );

  const reset = useCallback(() => {
    setQuery('');
    setActive(null);
    if (typeof items !== 'function') {
      setAllItems(items);
    }
  }, [items]);

  useEffect(() => {
    fetchItems('');
  }, [fetchItems]);

  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  return {
    flat,
    active,
    setActive,
    onInput,
    onKeyDown,
    reset,
    query,
    loading,
  };
}

export default useFilteredList;
