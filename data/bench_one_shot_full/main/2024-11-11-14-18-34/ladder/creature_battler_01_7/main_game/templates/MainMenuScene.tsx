import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, Power } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface GameStats {
    [key: string]: number;
}

interface GameMeta {
    prototype_id: string;
    category: string;
}

interface Skill {
    __type: "Skill";
    stats: {
        damage: number;
    };
    meta: GameMeta;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

interface Creature {
    __type: "Creature";
    stats: {
        hp: number;
        max_hp: number;
    };
    meta: GameMeta;
    entities: Record<string, any>;
    collections: {
        skills: Skill[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface Player {
    __type: "Player";
    stats: GameStats;
    meta: GameMeta;
    entities: Record<string, any>;
    collections: {
        creatures: Creature[];
    };
    uid: string;
    display_name: string;
    description: string;
}

interface GameUIData {
    __type: "MainMenuScene";
    stats: GameStats;
    meta: GameMeta;
    entities: {
        player: Player;
    };
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    return (
        <Card className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-800 to-slate-900 overflow-hidden">
            <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
                {/* Title Section with Image Container */}
                <div className="flex-1 flex items-center justify-center w-full max-w-2xl">
                    <div className="w-full h-48 bg-slate-700 rounded-lg flex items-center justify-center">
                        {/* Image container - actual image would be loaded via CSS or img tag */}
                        <span className="text-4xl font-bold text-white opacity-50">Game Title Image</span>
                    </div>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 w-full max-w-md mb-16">
                    {availableButtonSlugs.includes('play') && (
                        <Button
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="w-full flex items-center justify-center gap-2 text-xl"
                        >
                            <Play className="w-6 h-6" />
                            <span>Play Game</span>
                        </Button>
                    )}

                    {availableButtonSlugs.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            onClick={() => emitButtonClick('quit')}
                            className="w-full flex items-center justify-center gap-2 text-xl"
                        >
                            <Power className="w-6 h-6" />
                            <span>Quit</span>
                        </Button>
                    )}
                </div>
            </div>
        </Card>
    );
}
