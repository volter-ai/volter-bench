import {useCurrentButtons} from "@/lib/useChoices.ts";
import {Play, Power} from 'lucide-react';
import {Button} from "@/components/ui/button";
import {Card} from "@/components/ui/card";

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  collections: {
    creatures: BaseEntity[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons()

    if (!props.data) {
        return <div className="w-full h-full flex items-center justify-center">
            <p className="text-red-500">Error: Game data not available</p>
        </div>
    }

    return (
        <Card className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8">
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    {props.data.display_name || "Main Menu"}
                </h1>
            </div>

            {/* Button Section */}
            <div className="flex flex-col gap-4 mb-12 w-64">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="w-full flex items-center justify-center gap-2 bg-emerald-600 hover:bg-emerald-500"
                        size="lg"
                    >
                        <Play className="w-5 h-5" />
                        <span>Play Game</span>
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-500"
                        size="lg"
                        variant="destructive"
                    >
                        <Power className="w-5 h-5" />
                        <span>Quit</span>
                    </Button>
                )}
            </div>
        </Card>
    );
}
