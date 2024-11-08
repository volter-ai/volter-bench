import { useCurrentButtons } from "@/lib/useChoices";
import { Play, Power } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Stats {
    hp?: number;
    max_hp?: number;
    attack?: number;
    defense?: number;
    sp_attack?: number;
    sp_defense?: number;
    speed?: number;
    base_damage?: number;
}

interface Meta {
    prototype_id: string;
    category: string;
    creature_type?: string;
    skill_type?: string;
    is_physical?: boolean;
}

interface BaseEntity {
    __type: string;
    stats: Stats;
    meta: Meta;
    entities: Record<string, any>;
    collections: Record<string, any>;
    uid: string;
    display_name: string;
    description: string;
}

interface Skill extends BaseEntity {
    __type: "Skill";
}

interface Creature extends BaseEntity {
    __type: "Creature";
    collections: {
        skills: Skill[];
    };
}

interface Player extends BaseEntity {
    __type: "Player";
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
        <div className="w-full h-full relative">
            <div className="relative w-full pb-[56.25%]">
                <Card className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800 border-0">
                    <div className="flex-1 flex items-center justify-center">
                        <h1 className="text-6xl font-bold text-white tracking-wider">
                            {props.data?.display_name || "Game Title"}
                        </h1>
                    </div>

                    <div className="flex flex-col gap-4 w-full max-w-md">
                        {availableButtonSlugs.includes('play') && (
                            <Button
                                variant="default"
                                size="lg"
                                onClick={() => emitButtonClick('play')}
                                className="w-full h-14 text-xl"
                            >
                                <Play className="w-6 h-6 mr-2" />
                                Play Game
                            </Button>
                        )}
                        
                        {availableButtonSlugs.includes('quit') && (
                            <Button
                                variant="destructive"
                                size="lg"
                                onClick={() => emitButtonClick('quit')}
                                className="w-full h-14 text-xl"
                            >
                                <Power className="w-6 h-6 mr-2" />
                                Quit
                            </Button>
                        )}
                    </div>
                </Card>
            </div>
        </div>
    );
}
