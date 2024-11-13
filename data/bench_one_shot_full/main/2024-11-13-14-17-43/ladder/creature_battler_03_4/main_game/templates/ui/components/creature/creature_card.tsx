import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as ShadcnCard, 
  CardContent as ShadcnCardContent, 
  CardHeader as ShadcnCardHeader, 
  CardTitle as ShadcnCardTitle 
} from "@/components/ui/card"
import { Progress as ShadcnProgress } from "@/components/ui/progress"
import withClickable from "@/lib/withClickable"

// Custom components with uid
let Card = React.forwardRef<
  HTMLDivElement, 
  React.ComponentPropsWithRef<typeof ShadcnCard> & { uid: string }
>(({ uid, ...props }, ref) => <ShadcnCard ref={ref} {...props} />)

let CardHeader = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardHeader> & { uid: string }
>(({ uid, ...props }, ref) => <ShadcnCardHeader ref={ref} {...props} />)

let CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.ComponentPropsWithRef<typeof ShadcnCardTitle> & { uid: string }
>(({ uid, ...props }, ref) => <ShadcnCardTitle ref={ref} {...props} />)

let CardContent = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnCardContent> & { uid: string }
>(({ uid, ...props }, ref) => <ShadcnCardContent ref={ref} {...props} />)

let Progress = React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof ShadcnProgress> & { uid: string }
>(({ uid, ...props }, ref) => <ShadcnProgress ref={ref} {...props} />)

// Apply withClickable
Card = withClickable(Card)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)
CardContent = withClickable(CardContent)
Progress = withClickable(Progress)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  currentHp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, currentHp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[250px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="relative aspect-square w-full mb-4">
            <img
              src={imageUrl}
              alt={name}
              className="object-cover w-full h-full rounded-lg"
            />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm">HP</span>
              <span className="text-sm">{`${currentHp}/${maxHp}`}</span>
            </div>
            <Progress uid={`${uid}-progress`} value={(currentHp / maxHp) * 100} />
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
