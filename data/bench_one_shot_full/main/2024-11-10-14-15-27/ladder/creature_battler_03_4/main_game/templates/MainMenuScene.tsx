import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Skill {
    uid: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: string;
        skill_type: string;
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
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
    display_name: string;
    description: string;
}

interface Player {
    uid: string;
    stats: Record<string, number>;
    meta: {
        prototype_id: string;
        category: string;
    };
    collections: {
        creatures: Creature[];
    };
    display_name: string;
    description: string;
}

interface GameUIData {
    entities: {
        player: Player;
    };
    uid: string;
    display_name: string;
    description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    if (!props.data?.entities?.player) {
        return null;
    }

    return (
        <Card className="w-full h-full relative bg-gradient-to-b from-slate-900 to-slate-800 border-0">
            {/* 16:9 Aspect Ratio Container */}
            <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data.display_name || "GAME TITLE"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 items-center mb-12">
                    {availableButtonSlugs?.includes('play') && (
                        <Button
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="flex items-center gap-2 px-8 py-6 bg-emerald-600 hover:bg-emerald-500 
                                     text-white text-xl font-semibold"
                        >
                            <Play className="w-6 h-6" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            onClick={() => emitButtonClick('quit')}
                            className="flex items-center gap-2 px-8 py-6 
                                     text-white text-xl font-semibold"
                        >
                            <X className="w-6 h-6" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </Card>
    );
}
