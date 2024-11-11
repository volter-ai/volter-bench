import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface BaseEntity {
    __type: string;
    stats: Record<string, number>;
    meta: Record<string, string>;
    entities: Record<string, any>;
    collections: Record<string, any[]>;
    uid: string;
    display_name: string;
    description: string;
}

interface Skill extends BaseEntity {
    __type: "Skill";
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
        category: "Skill";
        skill_type: string;
    };
}

interface Creature extends BaseEntity {
    __type: "Creature";
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    meta: {
        prototype_id: string;
        category: "Creature";
        creature_type: string;
    };
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    __type: "Player";
    meta: {
        prototype_id: string;
        category: "Player";
    };
    collections: {
        creatures: Creature[];
    };
}

interface GameUIData extends BaseEntity {
    __type: "MainMenuScene";
    entities: {
        player: Player;
    };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    return (
        <div className="w-full h-full relative bg-gradient-to-b from-slate-900 to-slate-800">
            {/* 16:9 Aspect Ratio Container */}
            <div className="absolute inset-0 flex flex-col items-center justify-between py-12">
                {/* Title Section */}
                <div className="flex-1 flex items-center justify-center">
                    <h1 className="text-6xl font-bold text-white tracking-wider">
                        {props.data?.display_name || "GAME TITLE"}
                    </h1>
                </div>

                {/* Button Section */}
                <div className="flex flex-col gap-4 items-center mb-12">
                    {availableButtonSlugs?.includes('play') && (
                        <Button
                            variant="default"
                            size="lg"
                            onClick={() => emitButtonClick('play')}
                            className="w-48 h-16 text-xl"
                        >
                            <Play className="mr-2 h-6 w-6" />
                            Play Game
                        </Button>
                    )}

                    {availableButtonSlugs?.includes('quit') && (
                        <Button
                            variant="destructive"
                            size="lg"
                            onClick={() => emitButtonClick('quit')}
                            className="w-48 h-16 text-xl"
                        >
                            <X className="mr-2 h-6 w-6" />
                            Quit
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}
