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

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const getButtonIcon = (slug: string) => {
    switch (slug) {
      case 'play':
        return <Play className="mr-2 h-4 w-4" />;
      case 'quit':
        return <X className="mr-2 h-4 w-4" />;
      default:
        return null;
    }
  };

  return (
    <Card className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col justify-between items-center p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-6xl font-bold text-white text-center mt-16">
        Creature Adventure
      </h1>

      <div className="flex flex-col items-center mb-16">
        {availableButtonSlugs.map((slug) => (
          <Button
            key={slug}
            onClick={() => emitButtonClick(slug)}
            className="bg-white text-purple-700 hover:bg-purple-100 mb-4 w-48"
          >
            {getButtonIcon(slug)}
            {slug.charAt(0).toUpperCase() + slug.slice(1)}
          </Button>
        ))}
      </div>
    </Card>
  );
}
