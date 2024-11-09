import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

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

    return (
        <Card className="w-full h-full relative bg-gradient-to-b from-slate-900 to-slate-800 border-0">
            {/* 16:9 Aspect Ratio Container */}
            <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data?.display_name || "GAME TITLE"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 items-center mb-12 w-64">
                    {availableButtonSlugs?.includes('play') && (
                        <Button
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="w-full bg-emerald-600 hover:bg-emerald-500"
                        >
                            <Play className="mr-2 h-5 w-5" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            onClick={() => emitButtonClick('quit')}
                            className="w-full"
                        >
                            <X className="mr-2 h-5 w-5" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </Card>
    );
}
