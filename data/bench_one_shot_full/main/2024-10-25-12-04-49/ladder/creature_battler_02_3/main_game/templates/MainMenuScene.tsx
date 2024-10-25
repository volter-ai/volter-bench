import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    entities: Record<string, any>;
    collections: {
        creatures: Creature[];
    };
    display_name: string;
    description: string;
}

interface Creature {
    uid: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: string;
    };
    entities: Record<string, any>;
    collections: {
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Skill {
    uid: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
    };
    entities: Record<string, any>;
    collections: Record<string, any>;
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const playerName = props.data.entities.player?.display_name || 'Player';

    return (
        <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
            <div className="w-full h-full max-w-[177.78vh] max-h-[56.25vw] flex flex-col justify-between items-center p-8">
                <h1 className="text-4xl md:text-6xl font-bold text-white mt-8">
                    Creature Battle Game
                </h1>

                <div className="text-xl text-white">
                    Welcome, {playerName}!
                </div>

                <div className="flex flex-col space-y-4 mb-8">
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center justify-center px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-opacity-80 transition-colors"
                        >
                            <Play className="mr-2" size={24} />
                            Play Game
                        </Button>
                    )}
                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center justify-center px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-opacity-80 transition-colors"
                        >
                            <X className="mr-2" size={24} />
                            Quit Game
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}
