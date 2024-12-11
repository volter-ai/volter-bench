import * as React from "react"
import { cn } from "@/lib/utils"
import { 
  Card as BaseCard, 
  CardContent as BaseCardContent, 
  CardHeader as BaseCardHeader, 
  CardTitle as BaseCardTitle 
} from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = withClickable(React.forwardRef<
  HTMLDivElement, 
  React.ComponentPropsWithRef<typeof BaseCard> & BaseProps
>(({ uid, ...props }, ref) => (
  <BaseCard ref={ref} {...props} />
)))

let CardHeader = withClickable(React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof BaseCardHeader> & BaseProps
>(({ uid, ...props }, ref) => (
  <BaseCardHeader ref={ref} {...props} />
)))

let CardTitle = withClickable(React.forwardRef<
  HTMLParagraphElement,
  React.ComponentPropsWithRef<typeof BaseCardTitle> & BaseProps
>(({ uid, ...props }, ref) => (
  <BaseCardTitle ref={ref} {...props} />
)))

let CardContent = withClickable(React.forwardRef<
  HTMLDivElement,
  React.ComponentPropsWithRef<typeof BaseCardContent> & BaseProps
>(({ uid, ...props }, ref) => (
  <BaseCardContent ref={ref} {...props} />
)))

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  maxHp: number
  imageUrl: string
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, maxHp, imageUrl, ...props }, ref) => {
    return (
      <Card uid={`${uid}-card`} ref={ref} className={cn("w-[300px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
          <div className="text-sm text-muted-foreground">
            HP: {hp}/{maxHp}
          </div>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <img
            src={imageUrl}
            alt={name}
            className="w-full h-[200px] object-contain"
          />
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
