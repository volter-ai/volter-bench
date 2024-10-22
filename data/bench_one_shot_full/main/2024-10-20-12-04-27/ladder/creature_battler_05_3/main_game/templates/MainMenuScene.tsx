import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react'
import { Button } from "@/components/ui/button";

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex flex-col justify-between items-center p-8 bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="text-6xl font-bold text-white mt-16">
        Game Title
      </div>
      
      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.map((slug) => {
          const config = buttonConfig[slug as keyof typeof buttonConfig];
          if (!config) return null;
          
          return (
            <Button
              key={slug}
              onClick={() => emitButtonClick(slug)}
              className="w-48 h-12 text-lg flex items-center justify-center space-x-2"
            >
              <config.icon className="w-6 h-6" />
              <span>{config.text}</span>
            </Button>
          );
        })}
      </div>
    </div>
  );
}
