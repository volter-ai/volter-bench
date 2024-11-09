import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface GameEntity {
    uid: string;
    stats: Record<string, number>;
    meta: Record<string, string>;
    entities: Record<string, GameEntity>;
    collections: Record<string, any[]>;
    display_name: string;
    description: string;
}

interface Player extends GameEntity {
    collections: {
        creatures: GameEntity[];
    }
}

interface GameUIData {
    entities: {
        player: Player;
    };
    stats: Record<string, number>;
    meta: Record<string, string>;
    collections: Record<string, any[]>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    return (
        <div 
            className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8"
            key={props.data?.entities?.player?.uid ?? 'main-menu'}
        >
            {/* Title Section */}
            <div className="flex-1 flex items-center justify-center">
                <h1 className="text-6xl font-bold text-white tracking-wider">
                    CREATURE BATTLE
                </h1>
            </div>

            {/* Middle Spacer */}
            <div className="flex-1" />

            {/* Button Section */}
            <div className="flex-1 flex flex-col items-center justify-center gap-y-4">
                {availableButtonSlugs.includes('play') && (
                    <Button
                        onClick={() => emitButtonClick('play')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                        variant="default"
                        size="lg"
                    >
                        <Play className="w-6 h-6" />
                        Play Game
                    </Button>
                )}

                {availableButtonSlugs.includes('quit') && (
                    <Button
                        onClick={() => emitButtonClick('quit')}
                        className="flex items-center gap-x-2 px-8 py-6 text-xl"
                        variant="destructive"
                        size="lg"
                    >
                        <XCircle className="w-6 h-6" />
                        Quit
                    </Button>
                )}
            </div>
        </div>
    );
}
