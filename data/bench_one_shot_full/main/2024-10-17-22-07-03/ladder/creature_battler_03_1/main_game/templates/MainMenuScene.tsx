import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface GameUIData {
  entities: {
    player: {
      uid: string;
      stats: Record<string, number>;
      meta: Record<string, any>;
      entities: Record<string, any>;
      collections: Record<string, any[]>;
      display_name: string;
      description: string;
    };
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-full bg-gray-800 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      {/* Title Image Placeholder */}
      <div className="w-full h-1/3 bg-gray-700 flex items-center justify-center text-4xl font-bold text-white">
        {data.display_name || 'Game Title'}
      </div>

      {/* Buttons Section */}
      <div className="flex flex-col items-center space-y-4 mb-8">
        {availableButtonSlugs.map((slug) => {
          const button = buttonConfig[slug as keyof typeof buttonConfig];
          if (!button) return null;

          return (
            <button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded flex items-center space-x-2"
            >
              {button.icon && <button.icon size={24} />}
              <span>{button.text}</span>
            </button>
          );
        })}
      </div>

      {/* UID display for debugging purposes */}
      <div className="absolute bottom-2 right-2 text-xs text-gray-500">
        UID: {data.uid}
      </div>
    </div>
  );
}
