import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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

  const renderButton = (slug: string, icon: React.ReactNode, text: string) => {
    if (availableButtonSlugs.includes(slug)) {
      return (
        <Button
          key={slug}
          onClick={() => emitButtonClick(slug)}
          className="flex items-center justify-center"
        >
          {icon}
          <span className="ml-2">{text}</span>
        </Button>
      );
    }
    return null;
  };

  return (
    <Card className="w-full h-full bg-gray-800 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <div className="text-6xl font-bold text-white mt-16">
        Game Title
      </div>
      
      <div className="flex flex-col items-center space-y-4 mb-16">
        {renderButton('play', <Play className="h-4 w-4" />, 'Play')}
        {renderButton('quit', <X className="h-4 w-4" />, 'Quit')}
      </div>
    </Card>
  );
}
