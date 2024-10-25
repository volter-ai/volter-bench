import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const buttonConfig = {
    play: { icon: <Play className="mr-2 h-4 w-4" />, label: "Play" },
    quit: { icon: <X className="mr-2 h-4 w-4" />, label: "Quit" },
  };

  return (
    <div className="w-full h-screen bg-gradient-to-b from-purple-700 to-blue-900 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-6xl font-bold text-white mt-16">Game Title</h1>
      
      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          if (slug in buttonConfig) {
            const { icon, label } = buttonConfig[slug as keyof typeof buttonConfig];
            return (
              <Button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="w-48 flex items-center justify-center"
              >
                {icon}
                {label}
              </Button>
            );
          }
          return null;
        })}
      </div>
    </div>
  );
}
